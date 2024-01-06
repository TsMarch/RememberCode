//
//  QuestionTableInputDelegate.swift
//  code-start
//
//  Created by Тимур Калимуллин on 05.01.2024.
//

import Foundation

protocol QuestionTableInputDelegate: AnyObject {
    func countQA() -> Int
    func configureCell(index: Int) -> QAItem?
}

