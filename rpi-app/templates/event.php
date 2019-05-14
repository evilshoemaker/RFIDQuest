<?php 
	if(isset($_POST['add_team'])) {
		$arr = array(
			'player1' => $_POST['player1'], 
			'player2' => $_POST['player2'], 
			'player3' => $_POST['player3'], 
			'player4' => $_POST['player4'], 
			'player5' => $_POST['player5'],
			'player6' => $_POST['player6'],
			'player7' => $_POST['player7'],
			'player8' => $_POST['player8'],
			'player9' => $_POST['player9'],
			'player10' => $_POST['player10'],
		);
		echo json_encode($arr);

	}
	if(isset($_POST['clear_game'])) {
		/*$arr = array(
			'player1' => $_POST['player1'], 
			'player2' => $_POST['player2'], 
			'player3' => $_POST['player3'], 
			'player4' => $_POST['player4'], 
			'player5' => $_POST['player5'],
			'player6' => $_POST['player6'],
			'player7' => $_POST['player7'],
			'player8' => $_POST['player8'],
			'player9' => $_POST['player9'],
			'player10' => $_POST['player10'],
		);*/
		echo "На	й!!!!"; //json_encode($arr);

	}
?>