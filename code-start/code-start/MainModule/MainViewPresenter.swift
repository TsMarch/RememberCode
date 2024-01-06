//
//  MainViewPresenter.swift
//  code-start
//
//  Created by Тимур Калимуллин on 13.12.2023.
//

import Foundation
import UIKit

class MainViewPresenter: MainViewOutputDelegate {

    weak var moduleOutputDelegate: MainModuleOutputDelegate?

    func courseBlockTapped(courseName: String) {
        print(courseName)
        moduleOutputDelegate?.courseBlockTapped(courseName: courseName)
    }
}
