//
//  CourseItem.swift
//  code-start
//
//  Created by Тимур Калимуллин on 04.12.2023.
//

import Foundation
import UIKit

final class CourseItem {
    private(set) var courseName: String
    private(set) var isAvailable: Bool

    private(set) var color: UIColor
    private(set) var description: String
    private(set) var pictureName: String

    init(courseName: String, isAvailable: Bool = false, color: UIColor, description: String, pictureName: String) {
        self.courseName = courseName
        self.isAvailable = isAvailable

        self.color = color
        self.description = description
        self.pictureName = pictureName
    }
}


