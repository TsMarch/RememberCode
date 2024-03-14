//
//  LoginViewController.swift
//  code-start
//
//  Created by Тимур Калимуллин on 25.02.2024.
//

import UIKit

class LoginViewController: UIViewController {
    let loginView = LoginView()

    override func viewDidLoad() {
        super.viewDidLoad()
        view = loginView

        // Do any additional setup after loading the view.
    }
}
