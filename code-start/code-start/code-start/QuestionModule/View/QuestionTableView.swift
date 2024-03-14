//
//  QuestionTableView.swift
//  code-start
//
//  Created by Тимур Калимуллин on 05.01.2024.
//

import Foundation
import UIKit

class QuestionTableView: UIView {
    weak var delegate: QuestionTableOutputDelegate?
    
    let tableView = UITableView(frame: .zero, style: .plain)

    private lazy var questionLabel: UILabel = {
        let label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.text = "adasdsadsad"
        label.font = UIFont.systemFont(ofSize: 17)
        label.heightAnchor.constraint(equalToConstant: 44).isActive = true
        return label
    }()

    override init(frame: CGRect) {
        super.init(frame: frame)
        setupTableView()
        setupConstraints()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupTableView()
        setupConstraints()
    }

    private func setupTableView() {
        tableView.delegate = self
        tableView.dataSource = self
        tableView.register(QuestionCell.self, forCellReuseIdentifier: QuestionCell.identifier)
        tableView.translatesAutoresizingMaskIntoConstraints = false
        tableView.isPagingEnabled = true
        tableView.separatorStyle = .none
        tableView.bounces = false
        tableView.contentInset = UIEdgeInsets.zero
        tableView.contentInsetAdjustmentBehavior = .never
        tableView.allowsSelection = false
        tableView.rowHeight = UIScreen.main.bounds.height
        tableView.estimatedRowHeight = UIScreen.main.bounds.height
        tableView.widthAnchor.constraint(equalToConstant: UIScreen.main.bounds.width).isActive = true
        tableView.heightAnchor.constraint(equalToConstant: UIScreen.main.bounds.height).isActive = true

    }

    private func setupConstraints() {
        translatesAutoresizingMaskIntoConstraints = false
        backgroundColor = .white
        addSubview(tableView)

        NSLayoutConstraint.activate([
           tableView.topAnchor.constraint(equalTo: topAnchor),
           tableView.leadingAnchor.constraint(equalTo: leadingAnchor),
           tableView.trailingAnchor.constraint(equalTo: trailingAnchor),
           tableView.bottomAnchor.constraint(equalTo: bottomAnchor)
        ])

    }
}

extension QuestionTableView: UITableViewDelegate & UITableViewDataSource {
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        guard let cell = tableView.dequeueReusableCell(withIdentifier: QuestionCell.identifier, for: indexPath) as? QuestionCell else { fatalError() }
        //cell.backgroundColor = .blue

        if let item = delegate?.configureCell(index: indexPath.row) {
            cell.configure(item, indexPath.row)
            cell.delegate = self
        }
        return cell
    }

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return delegate?.countQA() ?? 0
    }
}

extension QuestionTableView: QuestionCellDelegate {
    public func deleteButtonTapped(row: Int) {
        delegate?.deleteButtonTapped(row: row)
    }

    public func favouriteButtonTapped(row: Int) {
        delegate?.favouriteButtonTapped(row: row)
    }
    

}

extension QuestionTableView: QuestionTableInputDelegate {
    public func deleteRow(row: Int) {
        tableView.deleteRows(at: [IndexPath(row: row, section: 0)], with: .fade)
        tableView.reloadData()
    }

    public func reconfigureRow(row: Int) {
        tableView.reconfigureRows(at: [IndexPath(row: row, section: 0)])
    }
}


