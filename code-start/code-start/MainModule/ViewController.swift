//
//  ViewController.swift
//  code-start
//
//  Created by Тимур Калимуллин on 04.12.2023.
//

import UIKit

class ViewController: UIViewController {
    let mainView = MainView()
    let presenter = MainViewPresenter()

    override func viewDidLoad() {
        super.viewDidLoad()
        navigationController?.navigationBar.isHidden = true
        view = mainView
        self.mainView.delegate = presenter
        // Do any additional setup after loading the view.
    }


}

