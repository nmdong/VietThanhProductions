//
//  SoundManager.swift
//  VietEduApp
//
//  Created by duynt0124 on 08/09/2023.
//

import AVFoundation

class SoundManager {
    
    static let shared = SoundManager()
    private var player: AVPlayer?
    private var speechSynthesizer: AVSpeechSynthesizer = AVSpeechSynthesizer()
        
    func playSound(fromURL urlString: String, completion: @escaping (Bool) -> Void) {
        if let encodedUrlString = urlString.addingPercentEncoding(withAllowedCharacters: .urlFragmentAllowed),
           let url = URL(string: encodedUrlString) {
            print("encodedUrlString: \(encodedUrlString)")
            let playerItem = AVPlayerItem(url: url)
            player = AVPlayer(playerItem: playerItem)

            // Add an observer to monitor when playback is finished
            NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: playerItem, queue: .main) { _ in
                // Playback finished
                completion(true)
            }

            player?.play()
            
        } else {
            print("Invalid URL: \(urlString)")
            completion(false)
        }
    }
    
    func playSound(fromURL urlString: String, times: Int, completion: @escaping (Bool) -> Void) {
        guard let url = URL(string: urlString), times > 0 else {
            completion(false)
            return
        }
        
        var playCount = 0
        
        func play() {
            player = AVPlayer(url: url)
            player?.play()
            
            NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: player?.currentItem, queue: .main) { _ in
                playCount += 1
                if playCount < times {
                    play()
                } else {
                    completion(true)
                }
            }
        }
        
        play()
    }

    
    func playLocalMP3(fileName: String) {
        guard let mp3FilePath = Bundle.main.path(forResource: fileName, ofType: "mp3") else {
            print("Local MP3 file not found: \(fileName)")
            return
        }
        
        let mp3URL = URL(fileURLWithPath: mp3FilePath)
        let playerItem = AVPlayerItem(url: mp3URL)
        player = AVPlayer(playerItem: playerItem)
        
        // Add an observer to monitor when playback is finished
        NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: playerItem, queue: .main) { _ in
            // Playback finished
        }
        
        player?.play()
    }
    
    func playSound(fromData data: Data, completion: @escaping (Bool) -> Void) {
        do {
            let audioSession = AVAudioSession.sharedInstance()
            try audioSession.setCategory(.playback)
            
            let tempFileURL = FileManager.default.temporaryDirectory.appendingPathComponent("temp_audio.mp3")
            
            try data.write(to: tempFileURL)
            
            let playerItem = AVPlayerItem(url: tempFileURL)
            
            // Check if there is an existing player, and if so, replace the current player item
            if let existingPlayer = player {
                existingPlayer.replaceCurrentItem(with: playerItem)
            } else {
                player = AVPlayer(playerItem: playerItem)
            }
            
            // Add an observer to monitor when playback is finished
            NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime, object: playerItem, queue: .main) { _ in
                // Playback finished
                completion(true)
            }
            
            player?.play()
        } catch {
            print("Failed to play sound from data: \(error.localizedDescription)")
            completion(false)
        }
    }
    
    func stopSound() {
        player?.pause()
        player = nil
        stopSpeechSynthesis()
    }
    
    func playSoundSpeechSynthesizer(str: String, localize: String = "en-US") {
        let speechUtterance = AVSpeechUtterance(string: str)
        
        if let voice = AVSpeechSynthesisVoice.init(language: localize) {
            speechUtterance.voice = voice
            speechUtterance.rate = 0.52
        }
        speechSynthesizer.speak(speechUtterance)
    }
    func stopSpeechSynthesis() {
        
        speechSynthesizer.stopSpeaking(at: .immediate)
    }
    
}
