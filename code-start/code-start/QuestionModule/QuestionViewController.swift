//
//  QuestionViewController.swift
//  code-start
//
//  Created by Тимур Калимуллин on 05.01.2024.
//

import Foundation
import UIKit

class QuestionViewController: UIViewController {
    private lazy var tableView = QuestionTableView()
    let presenter = QuestionViewPresenter()

    override func viewDidLoad() {
        super.viewDidLoad()
        view = tableView
        self.tableView.delegate = presenter
    }

}
