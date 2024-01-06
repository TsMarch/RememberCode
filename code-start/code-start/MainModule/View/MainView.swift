//
//  MainView.swift
//  code-start
//
//  Created by Тимур Калимуллин on 04.12.2023.
//

import UIKit

class MainView: UIView {
    weak var delegate: MainViewOutputDelegate?
    
    private lazy var upperStackView: UIStackView = {
        let stack = UIStackView()
        stack.axis = .horizontal
        stack.distribution = .fillProportionally
        stack.translatesAutoresizingMaskIntoConstraints = false
        return stack
    }()


    private lazy var profileButton: UIButton = {
        let button = UIButton()
        button.translatesAutoresizingMaskIntoConstraints = false
        button.heightAnchor.constraint(equalToConstant: 22).isActive = true
        button.setImage(UIImage(systemName: "person.crop.circle"), for: .normal)
        button.tintColor = UIColor.black
        button.contentVerticalAlignment = .fill
        button.contentHorizontalAlignment = .fill
        return button
    }()

    private lazy var profileLabel: UILabel = {
        let label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.text = "Good day, {profileUser}"
        label.font = UIFont.boldSystemFont(ofSize: Constans().headerFontSize)
        label.heightAnchor.constraint(equalToConstant: 22).isActive = true
        return label
    }()

    private lazy var notificationImage: UIImageView = {
        let image = UIImageView()
        image.translatesAutoresizingMaskIntoConstraints = false
        image.heightAnchor.constraint(equalToConstant: 22).isActive = true
        image.image = UIImage(systemName: "bell.fill")
        image.tintColor = UIColor.black
        return image
    }()

    private lazy var motivationLabel: UILabel = {
        let label = UILabel()
        label.text = Constans().motivationText
        label.translatesAutoresizingMaskIntoConstraints = false
        label.heightAnchor.constraint(equalToConstant: 42).isActive = true
        label.numberOfLines = 0
        return label
    }()

    private lazy var coursesStackView: UIStackView = {
        let stack = UIStackView()
        stack.translatesAutoresizingMaskIntoConstraints = false
        stack.axis = .vertical
        stack.spacing = 16

        return stack
    }()

    override init(frame: CGRect) {
        super.init(frame: frame)
        configureView()
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private func configureUpperStack() {
        upperStackView.addArrangedSubview(profileButton)
        upperStackView.setCustomSpacing(10, after: profileButton)
        upperStackView.addArrangedSubview(profileLabel)
        upperStackView.addArrangedSubview(notificationImage)


    }

    private func configureCoursesStack() {
        for course in Constans().courses {
            if let courseInfo = Constans().coursesInfo[course] {
                let courseView = CourseView(frame: .zero, name: courseInfo.courseName, color: courseInfo.color, descriptionCourse: courseInfo.description, pictureName: courseInfo.pictureName)
                courseView.delegate = self
                coursesStackView.addArrangedSubview(courseView)

            }
        }
    }

    private func configureView() {
        configureUpperStack()
        configureCoursesStack()
        backgroundColor = .white
        addSubview(upperStackView)
        addSubview(motivationLabel)
        addSubview(coursesStackView)

        NSLayoutConstraint.activate([
            upperStackView.topAnchor.constraint(equalTo: layoutMarginsGuide.topAnchor, constant: 34),
            upperStackView.leadingAnchor.constraint(equalTo: layoutMarginsGuide.leadingAnchor, constant: 10),
            upperStackView.trailingAnchor.constraint(equalTo: layoutMarginsGuide.trailingAnchor, constant: -10),

            motivationLabel.topAnchor.constraint(equalTo: upperStackView.bottomAnchor, constant: 14),
            motivationLabel.leadingAnchor.constraint(equalTo: layoutMarginsGuide.leadingAnchor,  constant: 10),
            motivationLabel.trailingAnchor.constraint(equalTo: layoutMarginsGuide.trailingAnchor, constant: -82),

            coursesStackView.topAnchor.constraint(equalTo: motivationLabel.bottomAnchor, constant: 29),
            coursesStackView.leadingAnchor.constraint(equalTo: layoutMarginsGuide.leadingAnchor),
            coursesStackView.trailingAnchor.constraint(equalTo: layoutMarginsGuide.trailingAnchor)
        ])

    }

}


extension MainView: CourseViewDelegate {
    func stackViewTapped(courseName: String) {
        delegate?.courseBlockTapped(courseName: courseName)
    }
}

extension MainView {
    struct Constans {
        let courses: [String] = ["python", "sql", "404"]

        let coursesInfo : [String: CourseItem] = [
            "python": CourseItem(courseName: "Python 3.0", isAvailable: true, color: #colorLiteral(red: 0.8118254542, green: 0.7447302938, blue: 0.8624684215, alpha: 1), description: "bibib babababa", pictureName: "brain.head.profile"),
            "sql" : CourseItem(courseName: "SQL", isAvailable: true, color: #colorLiteral(red: 0.9976977706, green: 0.6051780581, blue: 0.3850806355, alpha: 1), description: "bobob", pictureName: "light.ribbon.fill"),
            "404": CourseItem(courseName: "404", isAvailable: false, color: .gray, description: "coming soon", pictureName: "circle.dashed")]

        let fontSize: CGFloat = 14

        let headerFontSize: CGFloat = 18

        let motivationText: String = "Here some of the ways you can find help to grow in your studies"

    }
}


