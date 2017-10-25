# Knowledge: 0 (unfamiliar) or 1 (familiar)
rules = {
	'politics_us': {
		variation: {
			type: 'continuous',
			0 : 'Democrat',
			1 : 'Republican'
		},
		knowledge: 0,  # default no knowledge of topic 
		
		#actions: [
		#	'vote_us'
		#]
	}
}

societies = {
	id: 1, 
	name: "Optional", 
	rules: {				# Rules that the society follows... all populations generated here will have 						   knowledge of these rules (ie. knowledge =1 by default)
		
		'politics_us': [0,0.3]
		'', 
		''
	},  
}


# Actions 
# Later

