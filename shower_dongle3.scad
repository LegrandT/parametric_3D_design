difference() {
	linear_extrude(height = 9) {
		difference() {
			circle($fn = 72, r = 7.5);
			circle($fn = 72, r = 5.5);
		}
	}
	translate(v = [5, 0, 0]) {
		rotate(a = [0, 0, 45]) {
			translate(v = [-5.0, -5.0, -50]) {
				linear_extrude(height = 100) {
					square(size = 10);
				}
			}
		}
	}
}
