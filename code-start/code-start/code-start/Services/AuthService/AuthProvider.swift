//
//  AuthProvider.swift
//  code-start
//
//  Created by Тимур Калимуллин on 23.02.2024.
//

import Foundation

enum AuthProvider {
    case registration(RegistrationDTO)
    case token(LoginDTO) //login
}

extension AuthProvider: APIRequest {
    var baseURLString: String {
        return "178.154.204.204"
    }

    var apiPath: String {
        "auth"
    }

    var apiVersion: String? {
        nil
    }

    var separatorPath: String? {
        switch self {
        default:
            return nil
        }
    }

    var path: String {
        switch self {
        case .registration:
            return "registration/"
        case .token:
            return "token"
        }
    }

    var headers: [String : String]? {
        switch self {
        case .registration:
            return ["Content-Type": "application/json"]
        case .token:
            return ["Content-Type": "application/x-www-form-urlencoded"]
        }
    }

    var queryForCall: [URLQueryItem]? {
        switch self {
        default:
            return nil
        }
    }

    var params: [String : Any]? {
        switch self {
        case .registration(let request):
            return ["email": request.email, "nickname": request.nickname, "hashed_password": request.hashedPassword]
        case .token:
            return nil
        default:
            return nil
        }
    }

    var method: HTTPMethod {
        switch self {
        case .registration, .token:
            return .post
        }
    }

    var customDataBody: Data? {
        switch self {
        case .token(let request):
            return "username=\(request.username)&password=\(request.password)".data(using: .utf8)
        default:
            return nil
        }
    }
}
