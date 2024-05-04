//
//  APIRequest.swift
//  code-start
//
//  Created by Тимур Калимуллин on 23.02.2024.
//

import Foundation


protocol APIRequest {
    var baseURLString: String { get }
    var apiPath: String { get }
    var apiVersion: String? { get }
    var separatorPath: String? { get }
    var path: String { get }
    var headers: [String: String]? { get }
    var queryForCall: [URLQueryItem]? { get }
    var params: [String: Any]? { get }
    var method: HTTPMethod { get }
    var customDataBody: Data? { get }
}

extension APIRequest {
    var makeRequest: URLRequest {
        var urlComponents = URLComponents(string: baseURLString)
        urlComponents?.scheme = "http"
        urlComponents?.host = baseURLString

        var longPath = "/"
        longPath.append(apiPath)

        if let apiVersion = apiVersion {
            longPath.append("/")
            longPath.append(apiVersion)
        }

        if let separatorPath = separatorPath {
            longPath.append("/")
            longPath.append(separatorPath)
        }
        longPath.append("/")
        longPath.append(path)
        urlComponents?.path = longPath

        if let queryForCalls = queryForCall {
            urlComponents?.queryItems = [URLQueryItem]()
            for queryForCall in queryForCalls {
                urlComponents?.queryItems?.append(URLQueryItem(name: queryForCall.name, value: queryForCall.value))
            }
        }

        guard let url = urlComponents?.url else { return URLRequest(url: URL(string: baseURLString)!) }
        
        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue

        if let headers = headers {
            for header in headers {
                request.addValue(header.value, forHTTPHeaderField: header.key)
            }
        }

        if let params = params {
            let jsonData = try? JSONSerialization.data(withJSONObject: params)
            print(try? JSONSerialization.jsonObject(with: jsonData!) as? [String: Any])
            request.httpBody = jsonData
        }

        if let customDataBody = customDataBody {
            request.httpBody = customDataBody
        }
        
        return request
    }
}
