// Prints the tracks of an MP4 and saves frames at given times as PNG.
// usage: probe <file.mp4> <out dir> <t1,t2,…>   (built by ig-story.py with swiftc)
import AVFoundation
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
let asset = AVURLAsset(url: URL(fileURLWithPath: a[1]))
let sem = DispatchSemaphore(value: 0)
Task {
    let dur = try await asset.load(.duration)
    print("duration", String(format: "%.3f", dur.seconds))
    for t in try await asset.load(.tracks) {
        let (fmts, size, rate, fps, range) = try await t.load(.formatDescriptions, .naturalSize, .estimatedDataRate, .nominalFrameRate, .timeRange)
        let f = fmts.first!
        let sub = CMFormatDescriptionGetMediaSubType(f)
        let fourcc = String(bytes: [24, 16, 8, 0].map { UInt8((sub >> $0) & 0xff) }, encoding: .ascii) ?? "?"
        var extra = ""
        if t.mediaType == .audio, let asbd = CMAudioFormatDescriptionGetStreamBasicDescription(f)?.pointee { extra = "\(Int(asbd.mSampleRate)) Hz \(asbd.mChannelsPerFrame) ch" }
        if t.mediaType == .video, let ext = CMFormatDescriptionGetExtensions(f) as? [String: Any] { extra = ext.filter { $0.key.contains("Color") || $0.key.contains("Matrix") || $0.key.contains("Transfer") }.map { "\($0.key)=\($0.value)" }.sorted().joined(separator: " ") }
        print(t.mediaType.rawValue, fourcc, "\(Int(size.width))x\(Int(size.height))", String(format: "%.0f kbit/s", rate / 1000), String(format: "%.2f fps", fps), String(format: "start %.3f dur %.3f", range.start.seconds, range.duration.seconds), extra)
    }
    let gen = AVAssetImageGenerator(asset: asset)
    gen.requestedTimeToleranceBefore = .zero; gen.requestedTimeToleranceAfter = .zero
    for s in a[3].split(separator: ",") {
        let t = Double(s)!
        let (img, _) = try await gen.image(at: CMTime(seconds: t, preferredTimescale: 600))
        let url = URL(fileURLWithPath: a[2] + "/mp4-\(s).png")
        let d = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil)!
        CGImageDestinationAddImage(d, img, nil); CGImageDestinationFinalize(d)
    }
    sem.signal()
}
sem.wait()
