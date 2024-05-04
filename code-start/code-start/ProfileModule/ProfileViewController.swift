//
//  ProfileViewController.swift
//  code-start
//
//  Created by Тимур Калимуллин on 21.02.2024.
//

import UIKit

class ProfileViewController: UIViewController {
    let profileView = ProfileView()

    override func viewDidLoad() {
        super.viewDidLoad()
        view = profileView
        profileView.authStackView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(authViewTapped)))
    }

    @objc func authViewTapped() {
        let authViewController = AuthViewController()
        self.navigationController?.pushViewController(authViewController, animated: true)
    }
}
