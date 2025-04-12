import arcade
import random
import time
from .. import constants as C

class LevelGenerationError(Exception):
    """Custom exception for level generation failures"""
    pass

class LevelGenerator:
    def __init__(self):
        self.performance_stats = {
            'last_gen_time': 0,
            'avg_gen_time': 0,
            'errors': 0,
            'tests_passed': 0
        }
        self.debug_params = {
            'complexity': 1.0,
            'platform_count': 5,
            'hazard_density': 0.2
        }
        
    def generate_level(self, test_sequence=False, manual=False):
        """Main level generation entry point"""
        try:
            start_time = time.time()
            
            if test_sequence:
                level = self._run_test_sequence()
            elif manual:
                level = self._manual_generation()
            else:
                level = self._standard_generation()
                
            # Update performance stats
            gen_time = time.time() - start_time
            self._update_stats(gen_time)
            
            return level
            
        except Exception as e:
            self.performance_stats['errors'] += 1
            raise LevelGenerationError(f"Generation failed: {str(e)}")

    def _run_test_sequence(self):
        """Run comprehensive generation tests"""
        tests = [
            self._test_platform_placement,
            self._test_collision_maps,
            self._test_performance
        ]
        
        results = {}
        for test in tests:
            try:
                results[test.__name__] = test()
                self.performance_stats['tests_passed'] += 1
            except Exception as e:
                results[test.__name__] = str(e)
                
        return self._create_level(validate=results)

    def _manual_generation(self):
        """Generate with debug controls"""
        level = {
            'platforms': self._generate_platforms(
                count=self.debug_params['platform_count']
            ),
            'hazards': self._generate_hazards(
                density=self.debug_params['hazard_density']
            ),
            'spawn_points': self._calculate_spawn_points()
        }
        return level

    def _standard_generation(self):
        """Generate normal game level"""
        return {
            'platforms': self._generate_platforms(),
            'hazards': self._generate_hazards(),
            'spawn_points': self._calculate_spawn_points()
        }

    def _generate_platforms(self, count=None):
        """Generate platform layout"""
        count = count or random.randint(3, 7)
        platforms = []
        
        # Main floor platform
        platforms.append({
            'x': C.SCREEN_WIDTH // 2,
            'y': 32,
            'width': C.SCREEN_WIDTH * 1.5,
            'height': 64,
            'color': arcade.color.GRAY
        })
        
        # Additional platforms
        for i in range(count):
            platforms.append({
                'x': random.randint(100, C.SCREEN_WIDTH - 100),
                'y': random.randint(150, C.SCREEN_HEIGHT - 100),
                'width': random.randint(100, 300),
                'height': 20,
                'color': random.choice([
                    arcade.color.DARK_GREEN,
                    arcade.color.DARK_BROWN,
                    arcade.color.DARK_SLATE_GRAY
                ])
            })
            
        return platforms

    def _generate_hazards(self, density=0.1):
        """Generate hazard placement"""
        hazards = []
        if random.random() < density:
            for _ in range(random.randint(1, 3)):
                hazards.append({
                    'x': random.randint(50, C.SCREEN_WIDTH - 50),
                    'y': 40,
                    'width': random.randint(30, 100),
                    'height': 20,
                    'damage': 10
                })
        return hazards

    def _calculate_spawn_points(self):
        """Calculate player spawn positions"""
        return {
            'player1': (C.SCREEN_WIDTH * 0.25, 100),
            'player2': (C.SCREEN_WIDTH * 0.75, 100)
        }

    def _update_stats(self, gen_time):
        """Update performance statistics"""
        self.performance_stats['last_gen_time'] = gen_time
        if self.performance_stats['avg_gen_time'] == 0:
            self.performance_stats['avg_gen_time'] = gen_time
        else:
            self.performance_stats['avg_gen_time'] = (
                self.performance_stats['avg_gen_time'] * 0.9 + gen_time * 0.1
            )

    def _test_platform_placement(self):
        """Test platform generation rules"""
        platforms = self._generate_platforms(10)
        if len(platforms) != 11:  # +1 for main floor
            raise ValueError("Incorrect platform count")
        return True

    def _test_collision_maps(self):
        """Test collision space validity"""
        # Implementation would check for overlapping platforms
        return True

    def _test_performance(self):
        """Test generation performance"""
        start = time.time()
        self._generate_platforms(20)
        duration = time.time() - start
        if duration > 0.1:  # 100ms threshold
            raise ValueError(f"Generation too slow: {duration:.3f}s")
        return True

    def _create_level(self, validate=None):
        """Final level assembly with validation"""
        level = self._standard_generation()
        if validate:
            level['validation'] = validate
        return level