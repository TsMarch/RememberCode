//
//  QuestionViewPresenter.swift
//  code-start
//
//  Created by Тимур Калимуллин on 05.01.2024.
//

import Foundation

final class QuestionViewPresenter: QuestionTableOutputDelegate {
    private let qaCache: QACache

    private var questionToShow = [QAItem]()
    weak var delegate: QuestionTableInputDelegate?

    init() {
        qaCache = QACache()
        questionToShow = filterHiddenQuestion()
    }

    public func countQA() -> Int {
        return questionToShow.count
    }

    public func configureCell(index: Int) -> QAItem? {
        return questionToShow[index]
    }


    public func deleteButtonTapped(row: Int) {
        var item = questionToShow[row]
        item.setIsHidden(state: true)
        qaCache.addItem(item: item)
        questionToShow.remove(at: row)
        delegate?.deleteRow(row: row)
    }

    public func favouriteButtonTapped(row: Int) {
        var item = questionToShow[row]
        item.setIsFavourite(state: !item.getIsFavourite())
        qaCache.addItem(item: item)
        questionToShow[row] = item
        delegate?.reconfigureRow(row: row)
        print(questionToShow)
    }



}

extension QuestionViewPresenter {
    private func filterHiddenQuestion() -> [QAItem] {
        let filtredDict = qaCache.QAdict.filter { $0.value.getIsHidden() == false }
        return Array(filtredDict.values)
    }
}
