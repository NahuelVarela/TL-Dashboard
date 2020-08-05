<template>
	<v-card
	class="mx-auto">
	<v-list-item three-line>
      <v-list-item-content>
        <div class="overline mb-4">{{header}}</div>
        <v-list-item-title class="headline mb-1">{{title}}</v-list-item-title>
        <v-list-item-subtitle>{{subtitle}}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-card-actions>
      <v-btn v-on:click="start">Start</v-btn>
    </v-card-actions>

	</v-card>
</template>
<script>
export default {
	props: {
		header: String,
		title: String,
		subtitle: String,
		url: String,
	},
	methods:{
		start: function (){
			this.$http.get(this.url).then(function(response){
				if(response.status == "200"){
					console.log(response);
					window.alert(response);
				}
			})
		}
	}
}
</script>