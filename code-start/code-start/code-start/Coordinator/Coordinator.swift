//
//  Coordinator.swift
//  code-start
//
//  Created by Тимур Калимуллин on 13.12.2023.
//

import Foundation
import UIKit

protocol CoordinatorProtocol: AnyObject {
    func start()
    func finish()
}

final class AppCoordinator: NSObject, CoordinatorProtocol {
    private var navigationController: UINavigationController

    init(navigationController: UINavigationController) {
        self.navigationController = navigationController
    }

    func start() {
        let mainModuleBuilder = MainModuleBuilder()

        //let mainViewController = mainModuleBuilder.build(moduleOutput: self)
        let mainViewController = ViewController()
        mainViewController.presenter.moduleOutputDelegate = self
        //self.navigationController.pushViewController(mainViewController, animated: true)
        self.navigationController.pushViewController(mainViewController, animated: true)
    }

    func finish() {
    }
}

extension AppCoordinator: MainModuleOutputDelegate {
    func profileIconTapped() {
        let profileViewContoroller = ProfileViewController()
        self.navigationController.pushViewController(profileViewContoroller, animated: true)
    }

    func courseBlockTapped(courseName: String) {
        let questionViewController = QuestionViewController()
//        self.navigationController.definesPresentationContext = true
//        self.navigationController.providesPresentationContextTransitionStyle = true
//        questionViewController.definesPresentationContext = true
//        questionViewController.providesPresentationContextTransitionStyle = true
//        questionViewController.modalPresentationStyle = .popover
        self.navigationController.pushViewController(questionViewController, animated: true)
//        guard let vc = self.navigationController.topViewController else { return }
//        questionViewController.modalPresentationStyle = .overFullScreen
//       vc.present(questionViewController, animated: true)
    }
}
