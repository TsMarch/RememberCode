//
//  QuestionTableView.swift
//  code-start
//
//  Created by Тимур Калимуллин on 05.01.2024.
//

import Foundation
import UIKit

class QuestionTableView: UIView {
    weak var delegate: QuestionTableInputDelegate?
    
    let tableView = UITableView.init(frame: .zero, style: .plain)


    override init(frame: CGRect) {
        super.init(frame: frame)
        setupTableView()
        setupConstraints()
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    private func setupTableView() {
        tableView.delegate = self
        tableView.dataSource = self
        tableView.register(QuestionCell.self, forCellReuseIdentifier: QuestionCell.identifier)
        tableView.translatesAutoresizingMaskIntoConstraints = false
        tableView.isPagingEnabled = true
        tableView.layer.borderWidth = 10
        tableView.backgroundColor = .red
        tableView.rowHeight = 100
        tableView.heightAnchor.constraint(equalToConstant: 700).isActive = true
    }

    private func setupConstraints() {
        translatesAutoresizingMaskIntoConstraints = false
        backgroundColor = .white
        layer.borderWidth = 10
        addSubview(tableView)

        NSLayoutConstraint.activate([
//            tableView.centerXAnchor.constraint(equalTo: layoutMarginsGuide.centerXAnchor),
//            tableView.centerYAnchor.constraint(equalTo: layoutMarginsGuide.centerYAnchor)
           tableView.topAnchor.constraint(equalTo: self.topAnchor),
           tableView.leadingAnchor.constraint(equalTo: self.leadingAnchor),
            tableView.trailingAnchor.constraint(equalTo: self.trailingAnchor),
            tableView.bottomAnchor.constraint(equalTo: self.bottomAnchor)
        ])

    }
    
}

extension QuestionTableView: UITableViewDelegate & UITableViewDataSource {
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: QuestionCell.identifier, for: indexPath) as? QuestionCell else { fatalError() }
        cell.backgroundColor = .blue

        if let item = delegate?.configureCell(index: indexPath.row) {
            cell.configure(item)
        }
        return cell
    }

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        print(delegate?.countQA())
        return delegate?.countQA() ?? 0
    }
}


