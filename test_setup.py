#!/usr/bin/env python3
"""
Test script to verify the installation and setup.
"""
import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import pygame
        print("  ✓ pygame imported")
    except ImportError as e:
        print(f"  ✗ pygame import failed: {e}")
        return False
    
    try:
        import numpy
        print("  ✓ numpy imported")
    except ImportError as e:
        print(f"  ✗ numpy import failed: {e}")
        return False
    
    try:
        import torch
        print("  ✓ torch imported")
    except ImportError as e:
        print(f"  ✗ torch import failed: {e}")
        return False
    
    try:
        import matplotlib
        print("  ✓ matplotlib imported")
    except ImportError as e:
        print(f"  ✗ matplotlib import failed: {e}")
        return False
    
    return True


def test_project_structure():
    """Test that project structure is correct."""
    print("\nTesting project structure...")
    
    required_files = [
        'src/game/car.py',
        'src/game/track.py',
        'src/game/environment.py',
        'src/model/neural_network.py',
        'train.py',
        'play.py',
        'requirements.txt',
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✓ {file_path} exists")
        else:
            print(f"  ✗ {file_path} missing")
            all_exist = False
    
    return all_exist


def test_modules():
    """Test that custom modules can be imported."""
    print("\nTesting custom modules...")
    
    sys.path.insert(0, 'src')
    
    try:
        from game.car import Car
        print("  ✓ Car class imported")
    except ImportError as e:
        print(f"  ✗ Car import failed: {e}")
        return False
    
    try:
        from game.track import Track
        print("  ✓ Track class imported")
    except ImportError as e:
        print(f"  ✗ Track import failed: {e}")
        return False
    
    try:
        from game.environment import Environment
        print("  ✓ Environment class imported")
    except ImportError as e:
        print(f"  ✗ Environment import failed: {e}")
        return False
    
    try:
        from model.neural_network import CarNet, GeneticAlgorithm
        print("  ✓ CarNet and GeneticAlgorithm imported")
    except ImportError as e:
        print(f"  ✗ Neural network import failed: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality of key components."""
    print("\nTesting basic functionality...")
    
    sys.path.insert(0, 'src')
    
    try:
        from game.track import Track
        track = Track()
        assert len(track.waypoints) > 0, "Track has no waypoints"
        print("  ✓ Track creation works")
    except Exception as e:
        print(f"  ✗ Track creation failed: {e}")
        return False
    
    try:
        from game.car import Car
        car = Car(100, 100, 0)
        assert car.x == 100, "Car position not set correctly"
        assert car.alive == True, "Car should be alive initially"
        print("  ✓ Car creation works")
    except Exception as e:
        print(f"  ✗ Car creation failed: {e}")
        return False
    
    try:
        from model.neural_network import CarNet
        network = CarNet()
        import numpy as np
        state = np.zeros(6, dtype=np.float32)
        action = network.get_action(state)
        assert len(action) == 4, "Action should have 4 elements"
        print("  ✓ Neural network works")
    except Exception as e:
        print(f"  ✗ Neural network failed: {e}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("=" * 50)
    print("Self-Driving Car Setup Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Project Structure Test", test_project_structure),
        ("Custom Modules Test", test_modules),
        ("Basic Functionality Test", test_basic_functionality),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to start training.")
        print("\nNext steps:")
        print("  1. Try manual control: python play.py --mode manual")
        print("  2. Train the AI: python train.py")
        print("  3. Watch AI drive: python play.py --mode ai")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nTry running: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
