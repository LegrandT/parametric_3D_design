difference() {
	linear_extrude(height = 8) {
		difference() {
			circle($fn = 72, r = 8);
			circle($fn = 72, r = 6);
		}
	}
	translate(v = [-5, 0, -1]) {
		rotate(a = [0, 0, 45]) {
			translate(v = [-5, -5, -0.5]) {
				linear_extrude(height = 10) {
					square(size = 10);
				}
			}
		}
	}
}
