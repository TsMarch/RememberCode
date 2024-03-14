//
//  QuestionViewController.swift
//  code-start
//
//  Created by Тимур Калимуллин on 05.01.2024.
//

import Foundation
import UIKit

class QuestionViewController: UIViewController {
    let tableView = QuestionTableView()
    let presenter = QuestionViewPresenter()

    override func viewDidLoad() {
        super.viewDidLoad()
        view = tableView
        self.tableView.delegate = presenter
        presenter.delegate = self.tableView
        self.becomeFirstResponder()
    }
}
