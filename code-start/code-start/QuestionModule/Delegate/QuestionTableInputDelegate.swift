//
//  QuestionTableInputDelegate.swift
//  code-start
//
//  Created by Тимур Калимуллин on 08.01.2024.
//

import Foundation

protocol QuestionTableInputDelegate: AnyObject {
    func deleteRow(row: Int)
    func reconfigureRow(row: Int)
}
