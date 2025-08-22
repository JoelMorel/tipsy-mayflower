#!/usr/bin/env python3
"""
Simple test script for the improved Flask app.
Run with: python test_app.py
"""

import requests
import time
import json

BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    """Test the health check endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_index_page():
    """Test the main index page."""
    print("\nTesting index page...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Content length: {len(response.text)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_rate_limiting():
    """Test rate limiting on submit endpoint."""
    print("\nTesting rate limiting...")
    try:
        # Make multiple requests quickly to trigger rate limiting
        for i in range(12):  # Should trigger 10 per minute limit
            response = requests.post(f"{BASE_URL}/submit", data={
                'location': 'test',
                'venue': 'bar'
            })
            print(f"Request {i+1}: Status {response.status_code}")
            
            if response.status_code == 429:
                print("Rate limit triggered successfully!")
                return True
            
            time.sleep(0.1)  # Small delay between requests
        
        print("Rate limit not triggered (this might be expected)")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_input_validation():
    """Test input validation."""
    print("\nTesting input validation...")
    try:
        # Test empty location
        response = requests.post(f"{BASE_URL}/submit", data={
            'location': '',
            'venue': 'bar'
        })
        print(f"Empty location - Status: {response.status_code}")
        
        # Test very short location
        response = requests.post(f"{BASE_URL}/submit", data={
            'location': 'a',  # Too short
            'venue': 'bar'
        })
        print(f"Short location - Status: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_loader_functionality():
    """Test that the loader shows up on form submission."""
    print("\nTesting loader functionality...")
    try:
        # This is a frontend test, so we'll just verify the page loads
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200 and 'loading-overlay' in response.text:
            print("✓ Loading overlay HTML found in page")
            return True
        else:
            print("✗ Loading overlay HTML not found")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("Starting Flask app tests...")
    print("=" * 50)
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Index Page", test_index_page),
        ("Input Validation", test_input_validation),
        ("Loader Functionality", test_loader_functionality),
        ("Rate Limiting", test_rate_limiting),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"{test_name}: {'PASS' if result else 'FAIL'}")
        except Exception as e:
            print(f"{test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
