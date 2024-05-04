//
//  LoginViewController.swift
//  code-start
//
//  Created by Тимур Калимуллин on 03.04.2024.
//

import UIKit

class LoginViewController: UIViewController {
    weak var delegate: AuthViewControllerDelegate?
    private let service: AuthService = AuthService()
    private var username: String? = nil
    private var password: String? = nil

    private lazy var stackView: UIStackView = {
        let stack = UIStackView()
        stack.translatesAutoresizingMaskIntoConstraints = false
        stack.axis = .vertical
        stack.distribution = .fillEqually
        stack.spacing = 25
        return stack
    }()

    private lazy var forgotButton: UIButton = {
        let button = UIButton()
        button.translatesAutoresizingMaskIntoConstraints = false
        button.heightAnchor.constraint(equalToConstant: 22).isActive = true
        //button.widthAnchor.constraint(equalToConstant: 44).isActive = true
        button.setTitle("Forgot Password?", for: .normal)
        button.setTitleColor(UIColor.black, for: .normal)
        //button.titleLabel?.font = UIFont.boldSystemFont(ofSize: 12)
        return button
    }()

    private lazy var signInButton: UIButton = {
        let button = UIButton()
        button.translatesAutoresizingMaskIntoConstraints = false
        button.heightAnchor.constraint(equalToConstant: 22).isActive = true
        button.isEnabled = false
        button.setTitle("Sign In", for: .normal)
        button.setTitleColor(.gray, for: .normal)
        return button
    }()

    private lazy var closeButton: UIButton = {
        let button = UIButton()
        button.translatesAutoresizingMaskIntoConstraints = false
        button.heightAnchor.constraint(equalToConstant: 22).isActive = true
        button.widthAnchor.constraint(equalToConstant: 22).isActive = true
        button.setImage(UIImage(systemName: "chevron.left"), for: .normal)
        button.imageView?.tintColor = .lightGray
        button.imageView?.contentMode = .scaleAspectFit
        button.contentVerticalAlignment = .fill
        button.contentHorizontalAlignment = .fill
        return button
    }()

//    private lazy var closeButton: UIView = {
//        let view = UIView()
//        view.translatesAutoresizingMaskIntoConstraints = false
//        view.heightAnchor.constraint(equalToConstant: 3).isActive = true
//        view.widthAnchor.constraint(equalToConstant: 32).isActive = true
//        view.backgroundColor = .gray
//        ret
//    }()

    override func viewDidLoad() {
        super.viewDidLoad()
        self.setupView()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        delegate?.hideButtons()
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        delegate?.showButtons()
    }

    private func setupView() {
        //view.translatesAutoresizingMaskIntoConstraints = false
        view.backgroundColor = .white.withAlphaComponent(0.9)
        view.addSubview(stackView)
        view.addSubview(signInButton)
        view.addSubview(closeButton)

        NSLayoutConstraint.activate([
            stackView.centerYAnchor.constraint(equalTo: view.layoutMarginsGuide.centerYAnchor),
            stackView.leadingAnchor.constraint(equalTo: view.layoutMarginsGuide.leadingAnchor),
            stackView.trailingAnchor.constraint(equalTo: view.layoutMarginsGuide.trailingAnchor),

            signInButton.topAnchor.constraint(equalTo: view.layoutMarginsGuide.topAnchor, constant: 10),
            signInButton.trailingAnchor.constraint(equalTo: view.layoutMarginsGuide.trailingAnchor),

            closeButton.topAnchor.constraint(equalTo: view.layoutMarginsGuide.topAnchor, constant: 10),
            closeButton.leadingAnchor.constraint(equalTo: view.layoutMarginsGuide.leadingAnchor)
        ])

        self.setupStackView()
        self.setupTargets()
    }

    private func setupStackView() {
        for attribute in LoginAttributes.allCases {
            let view: UITextField = {
                let view = UITextField()
                view.placeholder = attribute.rawValue
                view.translatesAutoresizingMaskIntoConstraints = false
                view.heightAnchor.constraint(equalToConstant: 32).isActive = true
                view.font = UIFont.systemFont(ofSize: 20)
                view.layer.name = attribute.rawValue
                view.addTarget(self, action: #selector(textFieldDidChange(_:)), for: .editingChanged)
                let paddingView: UIView = UIView(frame: CGRect(x: 0, y: 0, width: 5, height: 20))
                view.leftView = paddingView
                view.leftViewMode = .always
                return view
            }()
            stackView.addArrangedSubview(view)
        }
    }

    private func setupTargets() {
        let tap = UITapGestureRecognizer(target: self, action: #selector(dismissKeyboard))
        view.addGestureRecognizer(tap)
        signInButton.addTarget(self, action: #selector(signInTapped), for: .touchUpInside)
        closeButton.addTarget(self, action: #selector(closeTapped), for: .touchUpInside)
    }

    @objc func textFieldDidChange(_ textField: UITextField) {
        guard let attribute = textField.layer.name,
        let data = textField.text?.trimmingCharacters(in: .whitespacesAndNewlines) else { return }
        switch LoginAttributes(rawValue: attribute) {
        case .password:
            password = data
        case .username:
            username = data
        default:
            break
        }

        if let username = username, let password = password {
            if username.isEmpty || password.isEmpty {
                disableButton()
            } else {
                enableButton()
            } 
        }
    }

    @objc func dismissKeyboard() {
        view.endEditing(true)
    }

    @objc func signInTapped() {
        guard let username = username, let password = password else { return }
        //Task {
        //    await service.loginUser(username: username, password: password)
        //}
        self.dismiss(animated: true)
        delegate?.successfullLoginPipeline()
    }

    @objc func closeTapped() {
        self.dismiss(animated: true)
    }

    private func applyBlur() {
        view.layoutIfNeeded()
        let blurEffect = UIBlurEffect(style: UIBlurEffect.Style.regular)
        let blurEffectView = UIVisualEffectView(effect: blurEffect)
        blurEffectView.frame = view.bounds
        blurEffectView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(blurEffectView)
    }
}

extension LoginViewController {
    public func getIcon(for field: LoginAttributes) -> UIImage? {
        switch field {
        case .password:
            return UIImage(systemName: "lock")
        case .username:
            return UIImage(systemName: "envelope")
        }
    }

    public func enableButton() {
        signInButton.setTitleColor(#colorLiteral(red: 0.1370271122, green: 0.8109224439, blue: 0.9838314652, alpha: 1), for: .normal)
        signInButton.isEnabled = true
    }

    public func disableButton() {
        signInButton.isEnabled = false
        signInButton.setTitleColor(.gray, for: .normal)
    }
}
