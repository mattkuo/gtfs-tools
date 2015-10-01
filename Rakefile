require 'rake/clean'

CLEAN.include('python/*.pyc', 'python/*.py', 'java/*.java')
CLEAN.exclude('python/__init__.py')
CLOBBER.include('output/*')

SRC = FileList['protos/*.proto']
BUILD_JAVA = 'java'
BUILD_PYTHON = 'python'

directory BUILD_JAVA
directory BUILD_PYTHON

task :default => [:java, :python]


SRC.each do |source|
	target = File.join(BUILD_JAVA, source.sub(/.proto$/, '.java'))
	file target => source do
		sh "java -jar wire.jar --java_out=. --proto_path=protos #{source.sub(/protos\//, '')}"
	end
	task :java => target
end

SRC.each do |source|
	target = File.join(BUILD_PYTHON, source.sub(/.proto$/, '_pb2.py'))
	file target => source do
		sh "protoc --python_out=#{BUILD_PYTHON} --proto_path=protos #{source}"
	end
	task :python => target
end
