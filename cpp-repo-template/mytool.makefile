all: meson nj
	echo noop

format:
	./tools/format-all

meson: 
	meson --default-library=static build-static .

remeson: 
	meson --reconfigure --default-library=static build-static .

nj:
	ninja -C build-static -v -j20 test |tee log

clean:
	rm -rf build-static
