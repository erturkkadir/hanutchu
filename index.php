<!DOCTYPE html>
<html lang="en">
	<title>Yapay Zeka Doktor Uygulaması</title>		
	<head>	
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Size özel YZ doktorunuzla karşılıklı sohbet edin</title>
	    
		<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" 
			rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" 
			crossorigin="anonymous">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
		<link rel="stylesheet" href="css/my.css">	
	
	</head>
	
	<body>

	<header>
		<a href="https://syshuman.com"><h1>sysHuman</h1></a>
	</header>

	<section id="hero" class="jumbotron jumbotron-fluid bg-primary text-white">
        <div class="containerBlurb">
            <h2 class="display-4">YZ doktorunuz ile sohbet edin</h2>
        </div>
    </section>
			
			<div class="row">
				<div class="col-sm-12">	
					<div class="panel panel-default form-control-lg">
				
					<form id="upload" role="form" action="dload.php" method="post" enctype="multipart/form-data">	
						<div class="col-sm-12">
							<div class="col-sm-12 text-center">
								<br>
								<h4  class="text-fail text-danger">
								Uyarı : Bu uygulama sadece tanıtım amaçlıdır. <br>
								Sonuçların doğruluğu hiçbir şekilde garanti edilmez.
								</h4>
								<br>
							</div>
						</div>
						<br/>						
					
						<p>"Başla" tuşuna basıp konuşmaya başlayın. </p>
						<div class="col-sm-6">						
							<button id="btnStart" name="btnStart" type="button" class="btn btn-primary btn-lg">
								<img src="images/mic.svg" alt="Bootstrap" />
								Başla</image>								
							</button> 
							<p id="sta" name="sta">Status</p> 
							<br/>
							<div class="input">
								<textarea type="text"  class="inputArea" rows="4" id="qry" name="qry" placeholder="" disabled> 
								</textarea>
							</div>
						</div>
						
						<div class="mb-4">							
							<input type="file" accept=".png,.jpg,.jpeg" id="img" name="img"></input> 
						</div>				
					</form>
					</div>
					
					<div class="output">
						<textarea type="text"  class="outputArea" rows="4" id="ans" name="ans" placeholder="" disabled> 
						</textarea>
					</div>
				</div>
			</div>
					
			<div class="container md-6">
				<footer class="bg-body-tertiary text-center text-white">
					<div class="p-8 pb-0">
						<a href="https://twitter.com/kadirerturk" class="fa fa-twitter"></a>
						<a href="https://www.youtube.com/@KadirErturk" class="fa fa-youtube"></a>
						<a href="https://www.linkedin.com/in/kadirerturk/" class="fa fa-linkedin"></a>
						<a href="https://www.github.com/erturkkadir" class="fa fa-github"></a>
						<a href="mailto:kadirerturk@gmail.com" class="fa fa-google"></a>						
					</div>
				</footer>
			</div>
		</div>	
		<audio id="voice" name="voice" controls> </audio>
		
		<script src="js/bootstrap.bundle.min.js"></script>
		
		<script src="js/listen.js" crossorigin="anonymous"></script>
		
		
	</body>
	
</html>