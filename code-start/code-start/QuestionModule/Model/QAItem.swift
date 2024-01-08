//
//  QAItem.swift
//  code-start
//
//  Created by Тимур Калимуллин on 13.12.2023.
//

import Foundation


struct QAItem {
    private let id: Int
    private let question: String
    private let answer: String
    private var isHidden: Bool
    private var isFavourite: Bool

    init(id: Int, question: String, answer: String, isHidden: Bool, isFavourite: Bool) {
        self.id = id
        self.question = question
        self.answer = answer
        self.isHidden = isHidden
        self.isFavourite = isFavourite
    }
    
    public func getId() -> Int {
        return id
    }

    public func getQuestion() -> String {
        return question
    }

    public func getAnswer() -> String {
        return answer
    }

    public func getIsHidden() -> Bool {
        return isHidden
    }

    public func getIsFavourite() -> Bool {
        return isFavourite
    }

    public mutating func setIsHidden(state: Bool) {
        self.isHidden = state
    }

    public mutating func setIsFavourite(state: Bool) {
        self.isFavourite = state
    }


}
