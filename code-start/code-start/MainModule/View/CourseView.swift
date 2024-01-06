//
//  CourseView.swift
//  code-start
//
//  Created by Тимур Калимуллин on 05.12.2023.
//

import Foundation
import UIKit

protocol CourseViewDelegate: AnyObject {
    func stackViewTapped(courseName: String)
}

class CourseView: UIView {
    let name: String
    let color: UIColor
    let descriptionCourse: String
    let pictureName: String

    weak var delegate: CourseViewDelegate?

    init(frame: CGRect, name: String, color: UIColor, descriptionCourse: String, pictureName: String) {
        self.name = name
        self.color = color
        self.descriptionCourse = descriptionCourse
        self.pictureName = pictureName
        super.init(frame: frame)
        
        configureView()
    }

    required init?(coder: NSCoder) {
            fatalError("init(coder:) has not been implemented")
    }


    private lazy var courseStackView: UIStackView = {
        let stack = UIStackView()
        stack.translatesAutoresizingMaskIntoConstraints = false
        stack.axis = .horizontal
        stack.heightAnchor.constraint(equalToConstant: 144).isActive = true
        stack.alignment = .center
        stack.distribution = .fillEqually
        return stack
    }()

    private lazy var leftStackView: UIStackView = {
        let stack = UIStackView()
        stack.translatesAutoresizingMaskIntoConstraints = false
        stack.heightAnchor.constraint(equalToConstant: 144).isActive = true
        stack.isLayoutMarginsRelativeArrangement = true
        stack.directionalLayoutMargins = NSDirectionalEdgeInsets(top: 31, leading: 12, bottom: 0, trailing: 0)
        stack.axis = .vertical
        stack.alignment = .fill
        stack.spacing = 9
        return stack
    }()

    private lazy var titleLabel: UILabel = {
        let label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.heightAnchor.constraint(equalToConstant: 22).isActive = true
        label.text = name
        label.font = UIFont.boldSystemFont(ofSize: Constans().headerFontSize)
        return label
    }()

    private lazy var descriptionLabel: VerticalTopAlignLabel = {
        let label = VerticalTopAlignLabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.text = descriptionCourse
        label.font = UIFont.systemFont(ofSize: Constans().fontSize)
        label.numberOfLines = 0

        return label
    }()

    private lazy var image: UIImageView = {
        let image = UIImageView()
        image.translatesAutoresizingMaskIntoConstraints = false
        image.heightAnchor.constraint(equalToConstant: 90).isActive = true
        image.image = UIImage(systemName: pictureName)
        image.tintColor = .gray
        image.contentMode = .scaleAspectFit

        image.layer.shadowColor = UIColor.black.cgColor
        image.layer.shadowOpacity = 5
        image.layer.shadowOffset = .zero
        image.layer.shadowRadius = 10
        
        return image
    }()

    private func configureStacks() {
        leftStackView.addArrangedSubview(titleLabel)
        leftStackView.addArrangedSubview(descriptionLabel)

        courseStackView.addArrangedSubview(leftStackView)
        courseStackView.addArrangedSubview(image)
    }

    private func configureView() {
        backgroundColor = color
        translatesAutoresizingMaskIntoConstraints = false
        layer.cornerRadius = 16
        configureStacks()
        addSubview(courseStackView)
        NSLayoutConstraint.activate([
            courseStackView.topAnchor.constraint(equalTo: topAnchor),
            courseStackView.bottomAnchor.constraint(equalTo: bottomAnchor),
            courseStackView.leadingAnchor.constraint(equalTo: leadingAnchor),
            courseStackView.trailingAnchor.constraint(equalTo: trailingAnchor)])

        courseStackView.addGestureRecognizer(UITapGestureRecognizer(target: self, action: #selector(stackViewTapped)))
    }



    @objc func stackViewTapped() {
        delegate?.stackViewTapped(courseName: name)
    }
}

extension CourseView {
    struct Constans {
        let fontSize: CGFloat = 14

        let headerFontSize: CGFloat = 18
    }
}

class VerticalTopAlignLabel: UILabel {
    override func drawText(in rect:CGRect) {
        guard let labelText = text else {  return super.drawText(in: rect) }

        let attributedText = NSAttributedString(string: labelText, attributes: [NSAttributedString.Key.font: font])
        var newRect = rect
        newRect.size.height = attributedText.boundingRect(with: rect.size, options: .usesLineFragmentOrigin, context: nil).size.height

        if numberOfLines != 0 {
            newRect.size.height = min(newRect.size.height, CGFloat(numberOfLines) * font.lineHeight)
        }

        super.drawText(in: newRect)
    }

}
