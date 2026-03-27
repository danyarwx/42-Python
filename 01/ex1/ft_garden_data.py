#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_garden_data.py                                    :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/27 23:23:22 by dzhukov             #+#    #+#            #
#   Updated: 2026/03/27 23:39:03 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

class Plant:
	def show(self):
		print(f"{self.name}: {self.height}cm, {self.age} days old")

def ft_garden_data():
	rose = Plant()
	rose.name = "Rose"
	rose.height = 25
	rose.age = 30
	sunflower = Plant()
	sunflower.name = "Sunflower"
	sunflower.height = 80
	sunflower.age = 45
	cactus = Plant()
	cactus.name = "Cactus"
	cactus.height = 15
	cactus.age = 120
	print("=== Garden Plant Registry ===")
	rose.show()
	sunflower.show()
	cactus.show()

if __name__ == "__main__":
	ft_garden_data()
