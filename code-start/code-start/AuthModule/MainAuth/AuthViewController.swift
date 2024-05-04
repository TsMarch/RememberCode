//
//  AuthViewController.swift
//  code-start
//
//  Created by Тимур Калимуллин on 25.02.2024.
//

import UIKit

protocol AuthViewControllerDelegate: AnyObject {
    func showButtons()
    func hideButtons()
    func successfullLoginPipeline()
}

class AuthViewController: UIViewController {
    let startAuthView = StartAuthView()

    override func viewDidLoad() {
        super.viewDidLoad()
        view = startAuthView
        startAuthView.singInButton.addTarget(self, action: #selector(singIn), for: .touchUpInside)
        startAuthView.singUpButton.addTarget(self, action: #selector(signUp), for: .touchUpInside)
    }

    @objc func singIn() {
        let loginViewController = LoginViewController()
        loginViewController.delegate = self
        loginViewController.modalPresentationStyle = .overFullScreen
        self.navigationController?.present(loginViewController, animated: true)
    }

    @objc func signUp() {
        let regViewController = RegistrationViewController()
        regViewController.delegate = self
        regViewController.modalPresentationStyle = .overFullScreen
        self.navigationController?.present(regViewController, animated: true)
    }
}

extension AuthViewController: AuthViewControllerDelegate {
    func successfullLoginPipeline() {
        self.navigationController?.popToRootViewController(animated: true)
    }

    func showButtons() {
        startAuthView.showButton()
    }
    func hideButtons() {
        startAuthView.hideButton()
    }
}
