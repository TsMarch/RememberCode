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
        return Date.now.timeIntervalSince1970 > accessToken.expiresAt && AuthUserDefaultsWorker.shared.haveAuthTokens()
    }

    public func requestAccessToken(with request: inout URLRequest) async {
        request.setValue(refreshToken.token, forHTTPHeaderField: "bearer")
        let data = try? await URLSession.shared.data(for: request)
        guard let binaryData = data?.0, let response = data?.1 as? HTTPURLResponse else { return }
        do {
            let decodedTokensInfo = try JSONDecoder().decode(TokenDTO.self, from: binaryData)
            print(decodedTokensInfo)
            updateTokens(tokensInfo: decodedTokensInfo)
        } catch {
            print(error)
        }
    }

    public func updateRequestTokenData(request: inout URLRequest) {
        request.setValue(accessToken.token, forHTTPHeaderField: "bearer")
    }

    public func updateTokens(tokensInfo: TokenDTO) {
        AuthUserDefaultsWorker.shared.saveAuthTokens(tokens: TokensInfo(from: tokensInfo))
        accessToken = AuthUserDefaultsWorker.shared.getAccessToken()
        refreshToken = AuthUserDefaultsWorker.shared.getRefreshToken()
    }
}
