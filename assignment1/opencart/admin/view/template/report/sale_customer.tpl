<?php echo $header; ?>
<div id="content">
	<div class="breadcrumb">
		<?php foreach ($breadcrumbs as $breadcrumb) { ?>
		<?php echo $breadcrumb['separator']; ?><a href="<?php echo $breadcrumb['href']; ?>"><?php echo $breadcrumb['text']; ?></a>
		<?php } ?>
	</div>
	<?php if ($error_install) { ?>
	<div class="warning"><?php echo $error_install; ?></div>
	<?php } ?>
	<?php if ($error_image) { ?>
	<div class="warning"><?php echo $error_image; ?></div>
	<?php } ?>
	<?php if ($error_image_cache) { ?>
	<div class="warning"><?php echo $error_image_cache; ?></div>
	<?php } ?>
	<?php if ($error_cache) { ?>
	<div class="warning"><?php echo $error_cache; ?></div>
	<?php } ?>
	<?php if ($error_download) { ?>
	<div class="warning"><?php echo $error_download; ?></div>
	<?php } ?>
	<?php if ($error_logs) { ?>
	<div class="warning"><?php echo $error_logs; ?></div>
	<?php } ?>
	<div class="box">
		<div class="heading">
			<h1><img src="view/image/customer.png" alt="" /> <?php echo $customer['firstname']; ?> <?php echo $customer['lastname']; ?></h1>
		</div>
		<div class="content">
			<div class="overview" style="width:100%">
				<div class="dashboard-heading"><?php echo $text_overview; ?></div>
				<div class="dashboard-content">
					<table>
						<tr>
							<td><?php echo $text_total_sale; ?></td>
							<td><?php echo $total_sale; ?></td>
						</tr>
						<tr>
							<td><?php echo $text_total_sale_year; ?></td>
							<td><?php echo $total_sale_year; ?></td>
						</tr>
						<tr>
							<td><?php echo $text_total_order; ?></td>
							<td><?php echo $total_order; ?></td>
						</tr>
						<tr>
							<td><?php echo $text_total_review_approval; ?></td>
							<td><?php echo $total_review_approval; ?></td>
						</tr>
						<tr>
							<td><?php echo $text_total_affiliate; ?></td>
							<td><?php echo $total_affiliate; ?></td>
						</tr>
						<tr>
							<td><?php echo $text_total_affiliate_approval; ?></td>
							<td><?php echo $total_affiliate_approval; ?></td>
						</tr>
					</table>
				</div>
			</div>
		</div>
		<div class="latest">
			<div class="dashboard-heading"><?php echo $text_latest_10_orders; ?></div>
			<div class="dashboard-content">
				<table class="list">
					<thead>
						<tr>
							<td class="right"><?php echo $column_order; ?></td>
							<td class="right"><?php echo $column_referral; ?></td>
							<td class="left"><?php echo $column_status; ?></td>
							<td class="left"><?php echo $column_date_added; ?></td>
							<td class="right"><?php echo $column_total; ?></td>
							<td class="right"><?php echo $column_action; ?></td>
						</tr>
					</thead>
					<tbody>
						<?php if ($orders) { ?>
						<?php foreach ($orders as $order) { ?>
						<tr>
							<td class="right"><?php echo $order['order_id']; ?></td>
							<td class="right"><?php echo $order['referral_id']; ?></td>
							<td class="left"><?php echo $order['status']; ?></td>
							<td class="left"><?php echo $order['date_added']; ?></td>
							<td class="right"><?php echo $order['total']; ?></td>
							<td class="right"><?php foreach ($order['action'] as $action) { ?>
								[ <a href="<?php echo $action['href']; ?>"><?php echo $action['text']; ?></a> ]
								<?php } ?></td>
							</tr>
							<?php } ?>
							<?php } else { ?>
							<tr>
								<td class="center" colspan="6"><?php echo $text_no_results; ?></td>
							</tr>
							<?php } ?>
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>
</div>
<!--[if IE]>
<script type="text/javascript" src="view/javascript/jquery/flot/excanvas.js"></script>
<![endif]--> 
<script type="text/javascript" src="view/javascript/jquery/flot/jquery.flot.js"></script> 
<?php echo $footer; ?>