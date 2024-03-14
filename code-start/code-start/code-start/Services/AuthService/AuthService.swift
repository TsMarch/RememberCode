//
//  AuthService.swift
//  code-start
//
//  Created by Тимур Калимуллин on 23.02.2024.
//

import Foundation

protocol AuthServiceProtocol: AnyObject {
    func registerUser(nickname: String, email: String, hashedPassword: String) async throws
}

class AuthService: AuthServiceProtocol {
    private let networkManager: NetworkManager

    init(networkManager: NetworkManager = NetworkManager()) {
        self.networkManager = networkManager
    }

    func registerUser(nickname: String, email: String, hashedPassword: String) async {
        let request = AuthProvider.registration(RegistrationDTO(nickname: nickname, email: email, hashedPassword: hashedPassword)).makeRequest
        let response = await networkManager.performRequest(request, decodingType: UserDTO.self)
        let data = response.0
        let responseStatus = response.1
    }

    func loginUser(username: String, password: String) async {
        let request = AuthProvider.token(LoginDTO(username: username, password: password)).makeRequest
        let response = await networkManager.performRequest(request, decodingType: TokenDTO.self)
        guard let data = response.0 else { return }
        Authenticator.shared.updateTokens(tokensInfo: data)
    }
}

extension AuthService {
    enum AuthServiceError: Error {
        case userAlreadyExist
        case userNotFound
    }
}

