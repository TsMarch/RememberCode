//
//  code_startTests.swift
//  code-startTests
//
//  Created by Тимур Калимуллин on 04.12.2023.
//

import XCTest
@testable import code_start

final class code_startTests: XCTestCase {

    override func setUpWithError() throws {
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }

    override func tearDownWithError() throws {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
    }

    func testExample() throws {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
        // Any test you write for XCTest can be annotated as throws and async.
        // Mark your test throws to produce an unexpected failure when your test encounters an uncaught error.
        // Mark your test async to allow awaiting for asynchronous code to complete. Check the results with assertions afterwards.
    }

    func testRegistraion() async {
        await AuthService().registerUser(nickname: "123tt", email: "tt@example.com", hashedPassword: "2313")

    }

    func testLoginUser() async {
        await AuthService().loginUser(username: "Timur", password: "Siska")
        await AuthService().testRoute()
    }


    func testRoute() async {
        await AuthService().testRoute()
    }

    func testRefreshRoute() async {
        await AuthService().refresh()
    }

    func testUserMe() async {
        await AuthService().userMeRoute()
    }

    func testPerformanceExample() throws {
        // This is an example of a performance test case.
        self.measure {
            // Put the code you want to measure the time of here.
        }
    }

}
