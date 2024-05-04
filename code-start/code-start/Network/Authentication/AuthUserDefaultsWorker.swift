//
//  AuthUserDefaultsWorker.swift
//  code-start
//
//  Created by Тимур Калимуллин on 14.03.2024.
//

import Foundation

class AuthUserDefaultsWorker {
    static let shared = AuthUserDefaultsWorker()

    private static let KEY_ACCESS_TOKEN = "auth_token"
    private static let KEY_ACCESS_TOKEN_EXPIRE = "auth_token_expire"
    private static let KEY_REFRESH_TOKEN = "refresh_token"
    private static let KEY_REFRESH_TOKEN_EXPIRE = "refresh_token_expire"

    func saveAuthTokens(tokens: TokensInfo) {
        let defaults = UserDefaults.standard
        defaults.set(tokens.accessToken, forKey: AuthUserDefaultsWorker.KEY_ACCESS_TOKEN)
        defaults.set(tokens.accessTokenExpire, forKey: AuthUserDefaultsWorker.KEY_ACCESS_TOKEN_EXPIRE)
        defaults.set(tokens.refreshToken, forKey: AuthUserDefaultsWorker.KEY_REFRESH_TOKEN)
        defaults.set(tokens.refreshTokenExpire, forKey: AuthUserDefaultsWorker.KEY_REFRESH_TOKEN_EXPIRE)
    }

    func getAccessToken() -> TokenInfo {
        let defaults = UserDefaults.standard
        let token = defaults.object(forKey: AuthUserDefaultsWorker.KEY_ACCESS_TOKEN) as? String ?? ""
        let expiresAt = defaults.object(forKey: AuthUserDefaultsWorker.KEY_ACCESS_TOKEN_EXPIRE) as? Double ?? 0
        return TokenInfo(token: token, expiresAt: expiresAt)
    }

    func getRefreshToken() -> TokenInfo {
        let defaults = UserDefaults.standard
        let token = defaults.object(forKey: AuthUserDefaultsWorker.KEY_REFRESH_TOKEN) as? String ?? ""
        let expiresAt = defaults.object(forKey: AuthUserDefaultsWorker.KEY_REFRESH_TOKEN_EXPIRE) as? Double ?? 0
        return TokenInfo(token: token, expiresAt: expiresAt)
    }

    func haveAuthTokens() -> Bool {
        return !getAccessToken().token.isEmpty && !getRefreshToken().token.isEmpty
    }

    func dropTokens() {
        let defaults = UserDefaults.standard
        defaults.set("", forKey: AuthUserDefaultsWorker.KEY_ACCESS_TOKEN)
        defaults.set(0 as Int64, forKey: AuthUserDefaultsWorker.KEY_ACCESS_TOKEN_EXPIRE)
        defaults.set("", forKey: AuthUserDefaultsWorker.KEY_REFRESH_TOKEN)
        defaults.set(0 as Int64, forKey: AuthUserDefaultsWorker.KEY_REFRESH_TOKEN_EXPIRE)
    }
}
