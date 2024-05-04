//
//  TokenDTO.swift
//  code-start
//
//  Created by Тимур Калимуллин on 25.02.2024.
//

import Foundation

struct TokenDTO: Decodable {
    let accessToken: String
    let refreshToken: String
    let accessTokenExpiration: String
    let refreshTokenExpiration: String

    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case accessTokenExpiration = "access_token_expiration"
        case refreshTokenExpiration = "refresh_token_expiration"
    }
}
