//
//  TokensInfo.swift
//  code-start
//
//  Created by Тимур Калимуллин on 14.03.2024.
//

import Foundation

struct TokensInfo {
    let accessToken: String
    let accessTokenExpire: Double
    let refreshToken: String
    let refreshTokenExpire: Double

    init(from token: TokenDTO) {
        self.accessToken = token.accessToken
        self.refreshToken = token.refreshToken
        let dateFormater = DateFormatter()
        dateFormater.dateFormat = "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"
        self.accessTokenExpire = dateFormater.date(from: token.accessTokenExpiration)?.timeIntervalSince1970 ?? 0
        self.refreshTokenExpire = dateFormater.date(from: token.refreshTokenExpiration)?.timeIntervalSince1970 ?? 0
        print(dateFormater.date(from: token.accessTokenExpiration))
    }
}

struct TokenInfo {
    let token: String
    let expiresAt: Double
}
