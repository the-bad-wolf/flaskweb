export default{
    install:function(Vue){
        Vue.directive('square',function(el,binding){
            el.innerHTML = Math.pow(binding.value,2)
        })
    }
}