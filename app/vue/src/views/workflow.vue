<template>
	<div class="workflow">
		<v-content>
			<v-container fluid>
				<v-row>
					<v-col v-for='flow in workflows' :key="flow.id">
						<Card 
						:header= "flow.header"
						:title="flow.title"
						:sub="flow.sub"
						:url="flow.url" />
					</v-col>
				</v-row>
			</v-container>
		</v-content>
	</div>
</template>

<script >
import Card from '../components/Card.vue'

export default {
	name: 'workflow',
	components:{
		Card
	},
	data () {
		return {
			workflows:[
			{id:1,
				header:"Workflow",
				title:"Automatic Exports",
				sub:"",
				url:"/rest/api/workflow/automatic_exports"},
			{id:2,
				header:"Workflow",
				title:"Automatic PFI Email",
				sub:"Send the PFI remainder Email",
				url:"/settings"},
			{id:3,
				header:"Workflow",
				title:"Automatic ",
				sub:"",
				url:"/settings"}]
		}
	}
}
</script>