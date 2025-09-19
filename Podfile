# Uncomment the next line to define a global platform for your project
platform :ios, '15.0'

target 'DemoData' do
  # Comment the next line if you don't want to use dynamic frameworks
  use_frameworks!
  pod 'IQKeyboardManager'
  pod 'SwifterSwift/UIKit'
  pod 'CRRefresh'
  pod 'SnapKit'
  pod 'R.swift'
  pod 'Alamofire', '~> 5.9'
  pod 'AlamofireImage', '~> 4.2'
end
  # Pods for DemoData
  post_install do |installer|
    installer.generated_projects.each do |project|
      project.targets.each do |target|
        target.build_configurations.each do |config|
          config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '15.0'
          config.build_settings['SWIFT_VERSION'] = '5.0'
        end
      end
    end
  end
