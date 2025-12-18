union() {
	color(alpha = 1.0, c = "red") {
		square(center = true, size = [10, 20]);
	}
	translate(v = [0, 0, 100]) {
		color(alpha = 1.0, c = "blue") {
			square(center = true, size = [20, 30]);
		}
	}
	hull() {
		color(alpha = 1.0, c = "red") {
			square(center = true, size = [10, 20]);
		}
		translate(v = [0, 0, 100]) {
			color(alpha = 1.0, c = "blue") {
				square(center = true, size = [20, 30]);
			}
		}
	}
}
