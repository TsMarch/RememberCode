//
//  Authenticator.swift
//  code-start
//
//  Created by Тимур Калимуллин on 14.03.2024.
//

import Foundation

class Authenticator {
    static let shared = Authenticator()
    
    private var accessToken = AuthUserDefaultsWorker.shared.getAccessToken()
    private var refreshToken = AuthUserDefaultsWorker.shared.getRefreshToken()
    
    public func isTokenExpire() -> Bool {
        print(Date.now.timeIntervalSince1970, accessToken.expiresAt)
        return Date().timeIntervalSince1970 > accessToken.expiresAt 
    }

    public func requestAccessToken() async {
        await AuthService().refresh()
    }

    public func updateRequestTokenData(request: inout URLRequest) {
        request.setValue("Bearer \(accessToken.token)", forHTTPHeaderField: "Authorization")
    }

    public func updateTokens(tokensInfo: TokenDTO) {
        AuthUserDefaultsWorker.shared.saveAuthTokens(tokens: TokensInfo(from: tokensInfo))
        accessToken = AuthUserDefaultsWorker.shared.getAccessToken()
        refreshToken = AuthUserDefaultsWorker.shared.getRefreshToken()
    }
}
