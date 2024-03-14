//
//  QuestionTableInputDelegate.swift
//  code-start
//
//  Created by Тимур Калимуллин on 05.01.2024.
//

import Foundation

protocol QuestionTableOutputDelegate: AnyObject {
    func countQA() -> Int
    func configureCell(index: Int) -> QAItem?
    func deleteButtonTapped(row: Int)
    func favouriteButtonTapped(row: Int)
}

