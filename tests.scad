union() {
	difference() {
		linear_extrude(height = 150, scale = 1.0, slices = 150.0, twist = 15.0) {
			union() {
				polygon(points = [[0, 50.0], [-43.30127018922193, -25.0], [43.30127018922193, -25.0]]);
				rotate(a = 60) {
					polygon(points = [[0, 50.0], [-43.30127018922193, -25.0], [43.30127018922193, -25.0]]);
				}
			}
		}
		color(alpha = 1.0, c = "red") {
			linear_extrude(height = 152, scale = 1.0, slices = 152.0, twist = 15.2) {
				offset($fn = 72, r = -2) {
					union() {
						polygon(points = [[0, 50.0], [-43.30127018922193, -25.0], [43.30127018922193, -25.0]]);
						rotate(a = 60) {
							polygon(points = [[0, 50.0], [-43.30127018922193, -25.0], [43.30127018922193, -25.0]]);
						}
					}
				}
			}
		}
	}
	linear_extrude(height = 2, scale = 1.0, slices = 2.0, twist = 0.2) {
		union() {
			polygon(points = [[0, 50.0], [-43.30127018922193, -25.0], [43.30127018922193, -25.0]]);
			rotate(a = 60) {
				polygon(points = [[0, 50.0], [-43.30127018922193, -25.0], [43.30127018922193, -25.0]]);
			}
		}
	}
}
