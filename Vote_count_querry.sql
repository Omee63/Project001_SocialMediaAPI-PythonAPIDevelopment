select posts.*, count(votes.post_id) as likes from posts left
join votes on posts.id = votes.post_id
group by posts.id;