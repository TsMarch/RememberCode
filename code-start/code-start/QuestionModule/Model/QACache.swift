//
//  QACache.swift
//  code-start
//
//  Created by Тимур Калимуллин on 13.12.2023.
//

import Foundation

final class QACache {
    private(set) var QAdict = [Int: QAItem]()

    init() {
        for i in 0..<10 {
            let item = QAItem(id: i, question: "sdasd", answer: "dasd", isHidden: false, isFavourite: false)
            addItem(item: item)
        }
    }

    public func addItem(item: QAItem) {
        if !QAdict.keys.contains(item.getId()) {
            QAdict[item.getId()] = item
        } else {
            QAdict.updateValue(item, forKey: item.getId())
        }

    }

    public func deleteItem(item: QAItem) {
        if QAdict.keys.contains(item.getId()) {
            QAdict.removeValue(forKey: item.getId())
        }
    }
}
