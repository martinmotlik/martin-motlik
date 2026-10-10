// Encodes PNG frames + a WAV track into an Instagram-ready MP4:
// H.264 High, 1080×1920, 30 fps, BT.709, ~20 Mbit/s; AAC-LC 44.1 kHz stereo 256 kbit/s.
// usage: encode <frames dir> <audio.wav> <out.mp4> <fps>   (built by ig-story.py with swiftc)
import AVFoundation
import CoreGraphics
import ImageIO
import Foundation

let args = CommandLine.arguments
let framesDir = URL(fileURLWithPath: args[1]), wavURL = URL(fileURLWithPath: args[2]), outURL = URL(fileURLWithPath: args[3])
let fps = Int32(args[4]) ?? 30
let W = 1080, H = 1920

let frames = try FileManager.default.contentsOfDirectory(atPath: framesDir.path).filter { $0.hasPrefix("f") && $0.hasSuffix(".png") }.sorted()
try? FileManager.default.removeItem(at: outURL)

let writer = try AVAssetWriter(outputURL: outURL, fileType: .mp4)
writer.shouldOptimizeForNetworkUse = true

let videoInput = AVAssetWriterInput(mediaType: .video, outputSettings: [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: W, AVVideoHeightKey: H,
    AVVideoColorPropertiesKey: [
        AVVideoColorPrimariesKey: AVVideoColorPrimaries_ITU_R_709_2,
        AVVideoTransferFunctionKey: AVVideoTransferFunction_ITU_R_709_2,
        AVVideoYCbCrMatrixKey: AVVideoYCbCrMatrix_ITU_R_709_2,
    ],
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: 20_000_000,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        AVVideoMaxKeyFrameIntervalKey: Int(fps),
        AVVideoExpectedSourceFrameRateKey: Int(fps),
        AVVideoAllowFrameReorderingKey: true,
        AVVideoH264EntropyModeKey: AVVideoH264EntropyModeCABAC,
    ],
])
videoInput.expectsMediaDataInRealTime = false
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: videoInput, sourcePixelBufferAttributes: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
    kCVPixelBufferWidthKey as String: W, kCVPixelBufferHeightKey as String: H,
])

let audioInput = AVAssetWriterInput(mediaType: .audio, outputSettings: [
    AVFormatIDKey: kAudioFormatMPEG4AAC,
    AVSampleRateKey: 44100, AVNumberOfChannelsKey: 2,
    AVEncoderBitRateKey: 256_000,
])
audioInput.expectsMediaDataInRealTime = false
writer.add(videoInput); writer.add(audioInput)

let asset = AVURLAsset(url: wavURL)
let reader = try AVAssetReader(asset: asset)
let sem = DispatchSemaphore(value: 0)
var audioTrack: AVAssetTrack?
Task { audioTrack = try await asset.loadTracks(withMediaType: .audio).first; sem.signal() }
sem.wait()
let audioOut = AVAssetReaderTrackOutput(track: audioTrack!, outputSettings: [
    AVFormatIDKey: kAudioFormatLinearPCM, AVLinearPCMBitDepthKey: 16, AVLinearPCMIsFloatKey: false,
    AVLinearPCMIsBigEndianKey: false, AVLinearPCMIsNonInterleaved: false,
])
reader.add(audioOut)

guard writer.startWriting(), reader.startReading() else { fatalError("start: \(String(describing: writer.error)) \(String(describing: reader.error))") }
writer.startSession(atSourceTime: .zero)

let srgb = CGColorSpace(name: CGColorSpace.sRGB)!
func pixelBuffer(_ path: String) -> CVPixelBuffer {
    let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil)!
    let img = CGImageSourceCreateImageAtIndex(src, 0, nil)!
    var pb: CVPixelBuffer?
    CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &pb)
    let buf = pb!
    CVBufferSetAttachment(buf, kCVImageBufferCGColorSpaceKey, srgb, .shouldPropagate)
    CVPixelBufferLockBaseAddress(buf, [])
    let ctx = CGContext(data: CVPixelBufferGetBaseAddress(buf), width: W, height: H, bitsPerComponent: 8,
                        bytesPerRow: CVPixelBufferGetBytesPerRow(buf), space: srgb,
                        bitmapInfo: CGImageAlphaInfo.premultipliedFirst.rawValue | CGBitmapInfo.byteOrder32Little.rawValue)!
    ctx.interpolationQuality = .none
    ctx.draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))
    CVPixelBufferUnlockBaseAddress(buf, [])
    return buf
}

let group = DispatchGroup()
let vq = DispatchQueue(label: "video"), aq = DispatchQueue(label: "audio")
var next = 0
group.enter()
videoInput.requestMediaDataWhenReady(on: vq) {
    while videoInput.isReadyForMoreMediaData {
        if next >= frames.count { videoInput.markAsFinished(); group.leave(); return }
        let buf = autoreleasepool { pixelBuffer(framesDir.appendingPathComponent(frames[next]).path) }
        if !adaptor.append(buf, withPresentationTime: CMTime(value: CMTimeValue(next), timescale: fps)) { fatalError("video append: \(String(describing: writer.error))") }
        next += 1
    }
}
group.enter()
audioInput.requestMediaDataWhenReady(on: aq) {
    while audioInput.isReadyForMoreMediaData {
        guard let sb = audioOut.copyNextSampleBuffer() else { audioInput.markAsFinished(); group.leave(); return }
        if !audioInput.append(sb) { fatalError("audio append: \(String(describing: writer.error))") }
    }
}
group.wait()
let done = DispatchSemaphore(value: 0)
writer.endSession(atSourceTime: CMTime(value: CMTimeValue(frames.count), timescale: fps))
writer.finishWriting { done.signal() }
done.wait()
if writer.status != .completed { fatalError("finish: \(String(describing: writer.error))") }
print("wrote \(outURL.path): \(frames.count) frames @ \(fps) fps")
