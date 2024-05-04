//
//  ProfileView.swift
//  code-start
//
//  Created by Тимур Калимуллин on 07.02.2024.
//

import UIKit

class ProfileView: UIView {
    lazy var authStackView: UIStackView = {
        let stack = UIStackView()
        stack.translatesAutoresizingMaskIntoConstraints = false
        stack.axis = .horizontal
        stack.distribution = .equalSpacing
        stack.alignment = .center
        stack.backgroundColor =  #colorLiteral(red: 0.9999879003, green: 0.9996979833, blue: 0.9906473756, alpha: 1)
        stack.layer.cornerRadius = 16
        stack.isLayoutMarginsRelativeArrangement = true
        stack.directionalLayoutMargins = NSDirectionalEdgeInsets(top: 16, leading: 15, bottom: 16, trailing: 5)
        return stack
    }()

    private lazy var profileIcon: UIButton = {
        let profileIcon = UIButton()
        profileIcon.translatesAutoresizingMaskIntoConstraints = false
        profileIcon.heightAnchor.constraint(equalToConstant: 44).isActive = true
        profileIcon.widthAnchor.constraint(equalToConstant: 44).isActive = true
        profileIcon.setImage(UIImage(systemName: "person.fill"), for: .normal)
        profileIcon.tintColor = .black
        profileIcon.backgroundColor = #colorLiteral(red: 0.8039215803, green: 0.8039215803, blue: 0.8039215803, alpha: 1)
        profileIcon.layer.cornerRadius = 22
        return profileIcon
    }()

    private lazy var infoStackView: UIStackView = {
        let stack = UIStackView()
        stack.translatesAutoresizingMaskIntoConstraints = false
        stack.axis = .vertical
        stack.distribution = .fillEqually
        stack.alignment = .leading
        return stack
    }()

    private lazy var accountInfo: UILabel = {
        let label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.text = Consts.placeholder
        label.font = UIFont.boldSystemFont(ofSize: 22)
        return label
    }()

    private lazy var accountDescription: UILabel = {
        let label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.text = Consts.placeholderDesctiption
        label.font = UIFont.systemFont(ofSize: 14)
        return label
    }()

    private lazy var chevronImageView: UIImageView = {
        let image = UIImageView()
        image.translatesAutoresizingMaskIntoConstraints = false
        image.heightAnchor.constraint(equalToConstant: 22).isActive = true
        image.widthAnchor.constraint(equalToConstant: 22).isActive = true
        image.image = UIImage(systemName: "chevron.right")
        image.tintColor = .gray
        image.contentMode = .scaleAspectFit
        return image
    }()

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupUI()
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private func setupUI() {
        authStackView.addArrangedSubview(profileIcon)

        infoStackView.addArrangedSubview(accountInfo)
        infoStackView.addArrangedSubview(accountDescription)
        authStackView.addArrangedSubview(infoStackView)
        authStackView.addArrangedSubview(chevronImageView)

        addSubview(authStackView)
        backgroundColor = #colorLiteral(red: 0.9848570228, green: 0.9807363153, blue: 0.9586277604, alpha: 1)

        NSLayoutConstraint.activate([
            authStackView.topAnchor.constraint(equalTo: self.layoutMarginsGuide.topAnchor),
            authStackView.leadingAnchor.constraint(equalTo: self.layoutMarginsGuide.leadingAnchor),
            authStackView.trailingAnchor.constraint(equalTo: self.layoutMarginsGuide.trailingAnchor)
        ])
    }
}


extension ProfileView {
    struct Consts {
        static let placeholder = "Create an account"

        static let placeholderDesctiption = "Already a member? Sign in"
    }
}
