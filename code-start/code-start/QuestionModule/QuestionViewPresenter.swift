//
//  QuestionViewPresenter.swift
//  code-start
//
//  Created by Тимур Калимуллин on 05.01.2024.
//

import Foundation

final class QuestionViewPresenter: QuestionTableInputDelegate {
    private let qaCache: QACache

    init() {
        qaCache = QACache()
    }

    func countQA() -> Int {
        return qaCache.QAdict.count
    }

    func configureCell(index: Int) -> QAItem? {
        let keyDict = Array(qaCache.QAdict.keys)[index]
        if let item = qaCache.QAdict[keyDict] {
            return item
        }
        return nil
    }
    
}
