
let junying = document.getElementById("junying");
//创建场景对象
let scene = new THREE.Scene();
// 设置光源
//点光源
let point = new THREE.PointLight(0xffffff);
point.position.set(500, 300, 300); //点光源位置
scene.add(point); //点光源添加到场景中
//环境光
let light = new THREE.AmbientLight(0x444444);
scene.add(light);
//相机设置
let camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);//透视摄像机
camera.position.set(0,50,350);//设置相机位置
camera.lookAt(scene.position);//设置相机方向(指向的场景对象)
// 加载模型
var loader = new THREE.GLTFLoader();
loader.load( 'BIM.glb', function ( glb ) {
	console.log(glb.scene);
	glb.scene.position.set(120,-400,0)
	scene.add(glb.scene);
}, undefined, function ( error ) {
	console.error( error );
} );

// 辅助坐标系  参数250表示坐标系大小，可以根据场景大小去设置
var axisHelper = new THREE.AxesHelper(250);
scene.add(axisHelper);


// 创建渲染对象
let renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);//设置渲染区域尺寸
renderer.setClearColor(0xb9d3ff, 1); //设置背景颜色
junying.appendChild(renderer.domElement)
// 执行渲染操作
function animate() {
    requestAnimationFrame(animate)
  renderer.render(scene,camera);//执行渲染操作
}

//创建控件对象
var controls = new THREE.OrbitControls(camera,renderer.domElement);


animate();
// setInterval("animate()",2000);