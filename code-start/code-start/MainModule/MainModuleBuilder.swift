//
//  MainModuleBuilder.swift
//  code-start
//
//  Created by Тимур Калимуллин on 13.12.2023.
//

import Foundation
import UIKit

class MainModuleBuilder{
    func build(moduleOutput: MainModuleOutputDelegate) -> UIViewController {
        let viewController = ViewController()
        let presenter = MainViewPresenter()
        viewController.mainView.delegate = presenter
        presenter.moduleOutputDelegate = moduleOutput
        return viewController
    }
}
